import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {MOCK_WHISPERS} from "./mock_whispers";
import {Whisper} from "./whispers/whisper";
import {ProfitableItem} from "./profitable-item";

@Injectable({
  providedIn: 'root'
})
export class WhisperServiceService {


  private url: string = `${window.location.protocol}//${window.location.hostname}/api/trades/whispers/`

  constructor(
    private http: HttpClient,
  ) {
  }

  getWhispers(items:ProfitableItem[]): Observable<Whisper[]> {
    const result = this.http.post<Whisper[]>(this.url,items);
    // const result = of(MOCK_WHISPERS);
    return result;
  }
}

