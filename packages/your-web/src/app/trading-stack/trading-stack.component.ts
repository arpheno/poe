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
    this.whisperService.direct_whisper(whisper.whisper_token,whisper.offer_count).subscribe(items=>console.log(items))
    this.newest_whisper=whisper;
    console.log(this.newest_whisper)
  }
  directWhisper(token:string,count:number) {
    console.log('whispering')
    this.whisperService.direct_whisper(token,count).subscribe(items=>console.log(items))
  }
}
