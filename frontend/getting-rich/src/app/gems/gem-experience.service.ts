import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";
import {GemExpModel} from "./gemExpModel";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class GemExperienceService {

  constructor(
    private http: HttpClient,
  ) {
  }

  private url: string = environment.gemExpUrl;
  getGemExperience(): Observable<GemExpModel[]> {
    let params = new HttpParams();
    const result = this.http.get<GemExpModel[]>(this.url, {params: params});
    // const result = of(MOCK_WHISPERS);
    return result;
  }
}
