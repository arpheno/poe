import {Component, Input, OnInit} from '@angular/core';
import {Whisper} from "./whisper";

@Component({
  selector: 'app-whispers',
  templateUrl: './whispers.component.html',
  styleUrls: ['./whispers.component.scss']
})
export class WhispersComponent implements OnInit {
  @Input() newWhispers:Whisper[] = [];
  newest_whisper: string='';

  constructor() { }

  ngOnInit(): void {
  }

  copyNewWhisper() {
    const whisper:Whisper = this.newWhispers.shift()!
    this.newest_whisper=whisper.whisper;
  }

  onKeyDown() {
    console.log('Copy Pressed');
  }
}

