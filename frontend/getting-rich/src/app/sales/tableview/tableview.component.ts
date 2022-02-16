import {Component, Input, OnInit, SimpleChanges, ViewChild} from '@angular/core';
import {Whisper} from "../../tradingview/whispers/whisper";
import {Result} from "../sales-serivce.service";
import {MatTableDataSource} from "@angular/material/table";
import {MatSort} from "@angular/material/sort";

@Component({
  selector: 'app-tableview',
  templateUrl: './tableview.component.html',
  styleUrls: ['./tableview.component.scss']
})
export class TableviewComponent implements OnInit {

  @Input() items:any;
  // @ts-ignore
  dataSource: MatTableDataSource<Result>;
  constructor() { }
  columnsToDisplay = [
    'type',
    'type_line',
    'initial_price',
    'stack_size',
    'simple_value',
    'config_value',
    'up_priced_value_fx',
    'final_price'
  ];
  @ViewChild(MatSort, {static: true}) sort!: MatSort;

  ngOnInit(): void {
  }
  ngOnChanges(changes: SimpleChanges) {
    let items=changes['items'].currentValue
    this.dataSource= new MatTableDataSource<Result>();
    this.dataSource.data=[...items]
    this.dataSource.sort = this.sort;
  }
}
