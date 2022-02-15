import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {environment} from "../../../environments/environment";
import {ProfitableItem} from "../../profitable-item";
import {Whisper} from "../whispers/whisper";

@Injectable({
  providedIn: 'root'
})
export class OrbOfHorizonServiceService {


  private url: string = environment.horizonUrl;

  constructor(
    private http: HttpClient,
  ) {
  }

  getOrbOfHorizonsSupply(): Observable<Whisper[]> {
    const result = this.http.get<Whisper[]>(this.url);
    console.log(result);
    return result;
  }
}

