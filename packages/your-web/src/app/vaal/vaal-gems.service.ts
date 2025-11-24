import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";

export interface VaalGemProfit {
  result: [{ name: string, profit: number }],
}

@Injectable({
  providedIn: 'root'
})
export class VaalGemsService {


  private url: string = environment.vaalurl;

  constructor(
    private http: HttpClient,
  ) {
  }

  resolve(): Observable<VaalGemProfit> {
    const result = this.http.get<VaalGemProfit>(this.url);
    return result;
  }
}
