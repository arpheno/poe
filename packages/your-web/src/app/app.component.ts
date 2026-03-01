import { Component } from '@angular/core';
import {Whisper} from "./tradingview/whispers/whisper";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'getting-rich';
  valuableItems: boolean = true;
  opened= true;

}
