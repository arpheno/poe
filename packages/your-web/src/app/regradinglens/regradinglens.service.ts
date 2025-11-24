import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";

export interface RegradinglensServiceReturn {
  result: [{
    "from": string,
    "basegem": string,
    "to": string,
    "value": number,
}]}

@Injectable({
  providedIn: 'root'
})
export class RegradinglensService {


  private url: string = environment.regradinglensurl;

  constructor(
    private http: HttpClient,
  ) {
  }

  resolve(): Observable<RegradinglensServiceReturn> {
    const result = this.http.get<RegradinglensServiceReturn>(this.url);
    return result;
  }
}
