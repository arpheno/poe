import { Component, OnInit } from '@angular/core';
import {Whisper} from "./whispers/whisper";

@Component({
  selector: 'app-tradingview',
  templateUrl: './tradingview.component.html',
  styleUrls: ['./tradingview.component.scss']
})
export class TradingviewComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  gWhispers: Whisper[]=[];
  onNewWhispers(event:Whisper[]) {
    console.log(event);
    let set_by_whisper_messages:any ={};
    for (let x of event){
      set_by_whisper_messages[x.whisper]=x;
    } for (let x of this.gWhispers){
      set_by_whisper_messages[x.whisper]=x;
    }
    this.gWhispers=Object.values(set_by_whisper_messages);
    this.gWhispers.sort((a,b)=>b.profit-a.profit);
  }
}
