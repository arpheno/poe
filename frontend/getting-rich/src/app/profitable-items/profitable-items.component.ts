import { Component, OnInit } from '@angular/core';
import {ProfitableItem} from "../profitable-item";
import {ProfitableItemService} from "../profitable-item.service";

@Component({
  selector: 'app-profitable-items',
  templateUrl: './profitable-items.component.html',
  styleUrls: ['./profitable-items.component.scss']
})
export class ProfitableItemsComponent implements OnInit {
  profitableItems: ProfitableItem[] = [];
  columnsToDisplay: string[] =['name','value','price','expected_profit'];

  constructor(private profitableItemService: ProfitableItemService) {
    this.getProfitableItems();
  }
  getProfitableItems(): void {
    this.profitableItemService.getProfitableItems()
      .subscribe(items => this.profitableItems = items);
  }

  ngOnInit(): void {
  }

}
