import { Injectable } from '@angular/core';
import {ProfitableItem} from "./profitable-item";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ProfitableItemService {
  private url: string ='http://localhost:8000/trades'
  constructor(
    private http: HttpClient,
  ) { }
  getProfitableItems(): Observable<ProfitableItem[]> {
    return this.http.get<ProfitableItem[]>(this.url);
    // return [{name:'Test Item',value:5,price:2,expectedProfit:3}];
  }
}
