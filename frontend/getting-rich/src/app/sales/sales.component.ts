import {Component, OnInit, ViewChild} from '@angular/core';
import {Result, SalesSerivceService} from "./sales-serivce.service";
import {MatTableDataSource} from "@angular/material/table";
import {MatSort} from "@angular/material/sort";

@Component({
  selector: 'app-sales',
  templateUrl: './sales.component.html',
  styleUrls: ['./sales.component.scss']
})
export class SalesComponent implements OnInit {
  private register: Result[] = [];

  dataSources:any={}
  @ViewChild(MatSort, {static: true}) sort!: MatSort;

  constructor(private salesService: SalesSerivceService) {
  }

  ngOnInit(): void {
    this.salesService.resolve().subscribe(items => {
      const types = Array.from(new Set(items.map(x=>x.type)));
      for (let x of types){
        this.dataSources[x]=[...items.filter(y=>y.type==x)]
      }
      console.log(this.dataSources)
      this.register = items;
      }
    )
  }

}
