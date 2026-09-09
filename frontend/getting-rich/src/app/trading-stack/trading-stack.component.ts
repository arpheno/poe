import {Component, Input, OnInit} from '@angular/core';
import {SearchResolveService, SearchResult} from "../search-resolve.service";
import {Whisper} from "../tradingview/whispers/whisper";
import {DirectWhisperService} from "../tradingview/whispers/direct-whisper.service";

@Component({
  selector: 'app-trading-stack',
  templateUrl: './trading-stack.component.html',
  styleUrls: ['./trading-stack.component.scss']
})
export class TradingStackComponent implements OnInit {

  @Input() query: { query: any } = {'query': {}}
  stack: any [] = [];
  newest_whisper: any = '';
  query_hash: string = '';
  action_error: string = '';

  constructor(private searchResolver: SearchResolveService,private whisperService:DirectWhisperService) {
  }

  ngOnInit(): void {
  }

  search_trades(): void {
    this.searchResolver.resolve(this.query).subscribe(x => {
      this.stack = x.result.sort((b,a)=>b.listing.price.amount-a.listing.price.amount);
      this.query_hash = x.query_hash;
      console.log(this.query_hash);
      console.log(this.stack);
    })
  }

  getFirstWhisper() {
    const whisper:Whisper = this.stack.shift()!.listing
    this.performTradeAction(whisper)
    this.newest_whisper=whisper;
    console.log(this.newest_whisper)
  }

  actionLabel(listing: Whisper): string {
    return listing.hideout_token ? 'Travel to Hideout' : 'Whisper Seller';
  }

  private performTradeAction(listing: Whisper) {
    this.action_error = '';
    if (listing.hideout_token) {
      this.whisperService.travel_to_hideout(listing.hideout_token).subscribe({
        next: items=>console.log(items),
        error: err => this.action_error = err.message
      })
      return;
    }
    this.whisperService.direct_whisper(listing.whisper_token, listing.offer_count).subscribe({
      next: items=>console.log(items),
      error: err => this.action_error = err.message
    })
  }
}
