import {Component, OnInit, ViewChild} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient, HttpParams} from "@angular/common/http";
import {ProfitableItem} from "../profitable-item";
import {Observable} from "rxjs";
import {Whisper} from "../tradingview/whispers/whisper";
import {GemExpModel} from "./gemExpModel";
import {GemExperienceService} from "./gem-experience.service";
import {MatTableDataSource} from "@angular/material/table";
import {MatSort} from "@angular/material/sort";
import {SearchResolveService} from "../search-resolve.service";

@Component({
  selector: 'app-gems',
  templateUrl: './gems.component.html',
  styleUrls: ['./gems.component.scss']
})
export class GemsComponent implements OnInit {

  dataSource = new MatTableDataSource<GemExpModel>();
  @ViewChild(MatSort, {static: true}) sort!: MatSort;
  columnsToDisplay = ['name','icon','xp_value','relative_profit', 'profit','price','actions'];
  private trades: any;

  constructor(private gemsExpService:GemExperienceService,private search_resolver:SearchResolveService) { }
  ngOnInit(): void {
    this.gemsExpService.getGemExperience().subscribe(items=>{
      console.log(items);
      this.dataSource.data = items;
      this.dataSource.sort = this.sort;

    })
  }


  getWhispers(row:any) {
    this.search_resolver.resolve(row.query).subscribe(x=>{
      this.trades[row.name]=x;
    })


  }
}
