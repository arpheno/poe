import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {map, Observable} from "rxjs";

export interface Result {
  chaos_value: number;
  type: string;
  type_line: string;
  initial_price: number;
  shoplink_template: string;
  stack_size: number;
  simple_value: number;
  config_value: number;
  temp_up_priced_value_fx: number;
  up_priced_value_fx: number;
  final_price_numerator: number;
  final_price_denominator: number;
}

export interface RootObject {
  result: Result[];
}
@Injectable({
  providedIn: 'root'
})
export class SalesSerivceService {


  private url: string = environment.registerUrl;

  constructor(
    private http: HttpClient,
  ){}

  resolve(): Observable<Result[]> {
    return this.http.get<RootObject>(this.url).pipe(map(x => x.result));
  }
}
