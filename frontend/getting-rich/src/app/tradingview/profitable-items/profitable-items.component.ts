import {Component, OnInit, Output, ViewChild, EventEmitter} from '@angular/core';
import {ProfitableItem} from "../../profitable-item";
import {ProfitableItemService} from "../profitable-item.service";
import {MatTableDataSource} from "@angular/material/table";
import {MatSort, Sort} from "@angular/material/sort";
import {LiveAnnouncer} from "@angular/cdk/a11y";
import {WhisperServiceService} from "../whisper-service.service";
import {Whisper} from "../whispers/whisper";

@Component({
  selector: 'app-profitable-items',
  templateUrl: './profitable-items.component.html',
  styleUrls: ['./profitable-items.component.scss']
})
export class ProfitableItemsComponent implements OnInit {
  @Output() generatedWhispers = new EventEmitter<Whisper[]>();
  profitableItems: ProfitableItem[] = [];
  columnsToDisplay: string[] = ['icon', 'name', 'value', 'price', 'expected_profit', 'relative_profit', 'actions'];
  dataSource = new MatTableDataSource<ProfitableItem>();
  @ViewChild(MatSort, {static: true}) sort!: MatSort;

  constructor(private profitableItemService: ProfitableItemService,
              private _liveAnnouncer: LiveAnnouncer,
              private whisperService: WhisperServiceService) {
  }

  getProfitableItems(): void {
    this.profitableItemService.getProfitableItems()
      .subscribe(items => {
        console.log(items);
        // this.profitableItems = items;
        this.dataSource.data = items;
        this.profitableItems = items;
        this.dataSource.sort = this.sort;

      });
  }

  /** Announce the change in sort state for assistive technology. */
  announceSortChange(sortState: Sort) {
    console.log(sortState);
    // This example uses English messages. If your application supports
    // multiple language, you would internationalize these strings.
    // Furthermore, you can customize the message to add additional
    // details about the values being sorted.
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }

  ngOnInit(): void {
    this.getProfitableItems();
  }

  getWhispers(item: ProfitableItem): void {
    console.log(item)
    this.whisperService.getWhispers([item])
      .subscribe(items => {
        console.log(items);
        this.generatedWhispers.emit(items);
        // this.profitableItems = items;

      });
  }

  onItemClicked() {
    console.log('lol')
  }

  allScarabs() {
    console.log(this.profitableItems)
    let asd = this.profitableItems.filter(x => x.name.endsWith('carab'));
    console.log(asd)
    this.whisperService.getWhispers(
      asd
    )
      .subscribe(items => {
        console.log(items);
        this.generatedWhispers.emit(items);
        // this.profitableItems = items;

      });

  }
}
