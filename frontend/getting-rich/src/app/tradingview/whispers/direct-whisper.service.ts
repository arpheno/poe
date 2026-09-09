import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable, of, throwError} from "rxjs";
import {catchError} from "rxjs/operators";
import {Whisper} from "./whisper";
import {ProfitableItem} from "../../profitable-item";
import {environment} from "../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class DirectWhisperService {


  private url: string = environment.whisperUrl;
  private whisper_url: string = environment.directWhisperUrl;

  constructor(
    private http: HttpClient,
  ) {
  }

  getWhispers(items: ProfitableItem[]): Observable<Whisper[]> {
    let params = new HttpParams();
    for (let item of items) {
      // @ts-ignore
      const item_as_params = {
        name: item.name,
        expected_profit: item.expected_profit.toFixed(2),
        value: item.value.toFixed(2)
      }
      params = params.appendAll(item_as_params);
      console.log(item);
      console.log(params);
    }
    const result = this.http.get<Whisper[]>(this.url, {params: params});
    // const result = of(MOCK_WHISPERS);
    return result;
  }

  direct_whisper(whisper_token: string, offer_count: number) {
    return this.sendTradeAction({token: whisper_token, values: [offer_count], action: 'whisper', game: 'poe1'});
  }

  travel_to_hideout(hideout_token: string) {
    // Triggers the official PoE 2 trade-site travel action endpoint; no in-game input automation.
    return this.sendTradeAction({token: hideout_token, hideout_token, action: 'travel_to_hideout', game: 'poe2'});
  }

  private sendTradeAction(payload: any) {
    return this.http.post<Whisper[]>(this.whisper_url, payload).pipe(
      catchError((error) => {
        const message =
          error?.error?.error?.message ||
          error?.error?.message ||
          error?.message ||
          'Trade action failed';
        return throwError(() => new Error(message));
      })
    );

  }
}
