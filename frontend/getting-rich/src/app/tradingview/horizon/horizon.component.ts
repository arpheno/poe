import { Component, OnInit } from '@angular/core';
import {OrbOfHorizonServiceService} from "./orb-of-horizon-service.service";
import {Whisper} from "../whispers/whisper";

@Component({
  selector: 'app-horizon',
  templateUrl: './horizon.component.html',
  styleUrls: ['./horizon.component.scss']
})
export class HorizonComponent implements OnInit {
  supply: Whisper[]=[];
  newest_whisper='';

  constructor(private horizonService:OrbOfHorizonServiceService) { }

  ngOnInit(): void {
    this.supply=[];
    this.horizonService.getOrbOfHorizonsSupply().subscribe(x=>{
      this.supply=x.sort(y=>-y.profit);
      console.log(this.supply)
      this.supply=this.supply.sort(y=>-y.profit)
    })

  }

  getNextHorizons() {
    this.newest_whisper=this.supply.shift()!.whisper;
  }
}
