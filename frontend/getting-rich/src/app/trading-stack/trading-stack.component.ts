import {Component, Input, OnInit} from '@angular/core';
import {SearchResolveService, SearchResult} from "../search-resolve.service";
import {Whisper} from "../tradingview/whispers/whisper";

@Component({
  selector: 'app-trading-stack',
  templateUrl: './trading-stack.component.html',
  styleUrls: ['./trading-stack.component.scss']
})
export class TradingStackComponent implements OnInit {

  @Input() query: { query: any } = {'query': {}}
  stack: any [] = [];
  newest_whisper: any = '';

  constructor(private searchResolver: SearchResolveService) {
  }

  ngOnInit(): void {
  }

  search_trades(): void {
    this.searchResolver.resolve(this.query).subscribe(x => {
      this.stack = x.result.sort((b,a)=>b.listing.price.amount-a.listing.price.amount);
      console.log(this.stack);
    })
  }

  getFirstWhisper() {
    this.newest_whisper = this.stack.shift()!.listing.whisper;
  }
}
