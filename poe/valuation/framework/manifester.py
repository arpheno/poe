from dataclasses import dataclass
from typing import Dict, Callable, List

import pendulum
from scipy import stats

from poe.valuation.framework.price_store import PriceStore
from poe.valuation.framework.transformationrule import TransformationRule
from poe.valuation.framework.valuation import Valuation
import numpy as np


from dataclasses import dataclass
from typing import Dict, Callable, List

import pendulum
from scipy import stats
import numpy as np

from poe.valuation.framework.price_store import PriceStore
from poe.valuation.framework.transformationrule import TransformationRule
from poe.valuation.framework.valuation import Valuation
from poe.valuation.framework.models import Ingredient, ItemQuery


@dataclass
class Manifester:
    prices: PriceStore

    def manifest(self, rule: TransformationRule) -> Valuation:
        # Calculate total cost of ingredients
        total_cost = 0
        concrete_ingredients = []
        
        for ingredient in rule.ingredients:
            candidates = self.prices.query(ingredient.query)
            if not candidates:
                return Valuation(
                    key=ingredient.query, 
                    estimate=0, 
                    timestamp=pendulum.now().int_timestamp, 
                    tags=['error'], 
                    info=f"Missing ingredient price: {ingredient.query}"
                )
            
            # Use the cheapest candidate for cost basis
            best_candidate = min(candidates, key=lambda x: x.estimate)
            concrete_ingredients.append(best_candidate)
            total_cost += best_candidate.estimate * ingredient.quantity

        # Calculate potential gains from products
        gains_values = []
        concrete_products = []
        
        for product_query in rule.products:
            candidates = self.prices.query(product_query)
            if not candidates:
                return Valuation(
                    key=rule.ingredients[0].query, 
                    estimate=0, 
                    timestamp=pendulum.now().int_timestamp, 
                    tags=['error'], 
                    info=f"Missing product price: {product_query}"
                )
            
            # Use the cheapest candidate (conservative estimate of sell price)
            best_product = min(candidates, key=lambda x: x.estimate)
            concrete_products.append(best_product)
            gains_values.append(best_product.estimate)

        gains = np.array(gains_values)
        probabilities = np.array(rule.probabilities)
        
        # Calculate statistics
        # Profit = Revenue - Cost
        # We calculate the distribution of (Revenue - Cost)
        profits = gains - total_cost
        
        # Aggregate duplicate profit values for rv_discrete
        unique_profits, inverse_indices = np.unique(profits, return_inverse=True)
        aggregated_probabilities = np.zeros_like(unique_profits, dtype=float)
        np.add.at(aggregated_probabilities, inverse_indices, probabilities)
        
        dist = stats.rv_discrete(name='value', values=(unique_profits, aggregated_probabilities))
        
        mean_profit = dist.mean() * rule.multiplier
        variance = dist.var() * rule.multiplier
        
        # Prepare breakdown data
        ingredients_breakdown = []
        for i, ingredient in enumerate(rule.ingredients):
            val = concrete_ingredients[i]
            ingredients_breakdown.append({
                "name": val.info or ingredient.query.name,
                "quantity": ingredient.quantity,
                "unit_cost": val.estimate,
                "total_cost": val.estimate * ingredient.quantity
            })
            
        products_breakdown = []
        expected_revenue = 0
        for i, product_query in enumerate(rule.products):
            val = concrete_products[i]
            prob = rule.probabilities[i]
            revenue = val.estimate * prob
            expected_revenue += revenue
            products_breakdown.append({
                "name": val.info or product_query.name,
                "probability": prob,
                "unit_value": val.estimate,
                "expected_revenue": revenue
            })
            
        breakdown = {
            "ingredients": ingredients_breakdown,
            "products": products_breakdown,
            "cost": total_cost,
            "revenue": expected_revenue,
            "profit": expected_revenue - total_cost,
            "multiplier": rule.multiplier,
            "scaled_profit": mean_profit
        }
        
        estimated_value = (total_cost * rule.multiplier) + mean_profit
        
        return Valuation(
            key=rule.ingredients[0].query,
            estimate=estimated_value,
            timestamp=pendulum.now().int_timestamp,
            info=f"{rule.info} | Profit: {mean_profit:.2f} | Risk: {np.sqrt(variance):.2f}",
            tags=rule.tags + ['rule', 'calculated'],
            breakdown=breakdown
        )

    def mean(self, costs: np.ndarray, gains: np.ndarray, probabilities: np.ndarray):
        return stats.rv_discrete(name='myvalue', values=(gains - np.sum(costs), probabilities)).mean()

    def variance(self, costs: np.ndarray, gains: np.ndarray, probabilities: np.ndarray):
        return stats.rv_discrete(name='myvalue', values=(gains - np.sum(costs), probabilities)).var()

    def map_to_concrete_items(self, funcs: [Callable]):
        # Deprecated
        pass
