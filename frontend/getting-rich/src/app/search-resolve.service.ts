import {Injectable} from '@angular/core';
import {environment} from "../environments/environment";
import {HttpClient, HttpParams} from "@angular/common/http";
import {ProfitableItem} from "./profitable-item";
import {Observable} from "rxjs";
import {Whisper} from "./tradingview/whispers/whisper";

export interface SearchResult{
  result:[{
    listing: { whisper: any, price: { amount: number, currency: string } };
  }],
  query_hash:string
}
@Injectable({
  providedIn: 'root'
})
export class SearchResolveService {


  private url: string = environment.search_resolve_url;

  constructor(
    private http: HttpClient,
  ){}

  resolve(query: any): Observable<SearchResult> {
    const result = this.http.post<SearchResult>(this.url, query);
    return result;
  }
}

