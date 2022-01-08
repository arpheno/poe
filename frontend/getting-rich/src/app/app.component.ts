import { Component } from '@angular/core';
import {Whisper} from "./whispers/whisper";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'getting-rich';
  gWhispers: Whisper[]=[];

  onNewWhispers(event:Whisper[]) {
    console.log(event);
    this.gWhispers.push(...event);
    this.gWhispers.sort((a,b)=>b.profit-a.profit);
  }
}
