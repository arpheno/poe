import { Injectable } from '@angular/core';
import {ProfitableItem} from "./profitable-item";
import {HttpClient} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {MOCK_ITEMS} from "./profitable-items/mock_items";

@Injectable({
  providedIn: 'root'
})
export class ProfitableItemService {
  private url: string ='http://localhost:8000/trades'
  constructor(
    private http: HttpClient,
  ) { }
  getProfitableItems(): Observable<ProfitableItem[]> {
    const result = this.http.get<ProfitableItem[]>(this.url);
    // const result = of(MOCK_ITEMS);
    return result;

    // return [{name:'Test Item',value:5,price:2,expectedProfit:3}];
  }
}
