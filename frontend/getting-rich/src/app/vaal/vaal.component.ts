import {Component, OnInit, ViewChild} from '@angular/core';
import {VaalGemProfit, VaalGemsService} from "./vaal-gems.service";
import {MatTableDataSource} from "@angular/material/table";
import {GemExpModel} from "../gems/gemExpModel";
import {MatSort} from "@angular/material/sort";

@Component({
  selector: 'app-vaal',
  templateUrl: './vaal.component.html',
  styleUrls: ['./vaal.component.scss']
})
export class VaalComponent implements OnInit {

  dataSource = new MatTableDataSource<{name:string,profit:number}>();
  @ViewChild(MatSort, {static: true}) sort!: MatSort;
  columnsToDisplay = ['name','profit'];
  constructor(private vaalGemService:VaalGemsService) { }

  ngOnInit(): void {
    this.vaalGemService.resolve().subscribe(items=>{
      console.log(items);
      this.dataSource.data = items.result;
      this.dataSource.sort = this.sort;

    })
  }

}
