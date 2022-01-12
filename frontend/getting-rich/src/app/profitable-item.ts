export interface ProfitableItemConstructorParams {
  name: string;
  value: number;
  price: number;
  expected_profit: number;
  icon: string;
  explicit_mods: ExplictModifier[];
}

export interface ExplictModifier {
  text: string,
  optional: boolean
}

export class ProfitableItem {
  get relative_profit(): number {
    return this.expected_profit / this.price;
  }

  get explicit_modifiers(): string {
    return this.explicit_mods.map(x => x['text']).join('\n')
  }

  explicit_mods: ExplictModifier[];
  name: string;
  value: number;
  price: number;
  expected_profit: number;
  icon: string;

  constructor({name, value, price, expected_profit, icon, explicit_mods}: ProfitableItemConstructorParams) {
    this.name = name;
    this.value = value;
    this.price = price;
    this.expected_profit = expected_profit;
    this.icon = icon;
    if (explicit_mods != null) {
      this.explicit_mods = explicit_mods;
    } else {
      this.explicit_mods = [];
    }
  }

}
