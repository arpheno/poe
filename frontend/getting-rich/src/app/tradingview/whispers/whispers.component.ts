import {Component, Input, OnInit} from '@angular/core';
import {Whisper} from "./whisper";
import {WhisperServiceService} from "../whisper-service.service";
import {DirectWhisperService} from "./direct-whisper.service";

@Component({
  selector: 'app-whispers',
  templateUrl: './whispers.component.html',
  styleUrls: ['./whispers.component.scss']
})
export class WhispersComponent implements OnInit {
  @Input() newWhispers:Whisper[] = [];
  newest_whisper: string='';

  constructor(  private whisperService: DirectWhisperService) { }

  ngOnInit(): void {
  }

  copyNewWhisper() {
    const whisper:Whisper = this.newWhispers.shift()!
    this.whisperService.direct_whisper(whisper.whisper_token,whisper.offer_count).subscribe(items=>console.log(items))
    this.newest_whisper=whisper.whisper;
  }

  onKeyDown() {
    console.log('Copy Pressed');
  }
  private percentColors = [
    { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
    { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
    { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } } ];

  getColorForPercentage(pct:number) {
    for (var i = 1; i < this.percentColors.length - 1; i++) {
      if (pct < this.percentColors[i].pct) {
        break;
      }
    }
    var lower = this.percentColors[i - 1];
    var upper = this.percentColors[i];
    var range = upper.pct - lower.pct;
    var rangePct = (pct - lower.pct) / range;
    var pctLower = 1 - rangePct;
    var pctUpper = rangePct;
    var color = {
      r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
      g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
      b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
    };
    return 'rgb(' + [color.r, color.g, color.b].join(',') + ')';
    // or output as hex if preferred
  };

  directWhisper(token:string,count:number) {
    console.log('whispering')
    this.whisperService.direct_whisper(token,count).subscribe(items=>console.log(items))
  }
}

