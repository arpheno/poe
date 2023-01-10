import {Component, OnInit, ViewChild} from '@angular/core';
import {RegradinglensService} from "./regradinglens.service";
import {MatTableDataSource} from "@angular/material/table";
import {MatSort} from "@angular/material/sort";

@Component({
  selector: 'app-regradinglens',
  templateUrl: './regradinglens.component.html',
  styleUrls: ['./regradinglens.component.scss']
})
export class RegradinglensComponent implements OnInit {



  dataSource = new MatTableDataSource<{basegem:string,value:number}>();
  @ViewChild(MatSort, {static: true}) sort!: MatSort;
  columnsToDisplay = ['basegem','value'];
  constructor(private regradinglensService:RegradinglensService) { }

  ngOnInit(): void {
    this.regradinglensService.resolve().subscribe(items=>{
      console.log(items);
      this.dataSource.data = items.result;
      this.dataSource.sort = this.sort;

    })
  }


}
