import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HttpClientModule} from "@angular/common/http";
import {ProfitableItemsComponent} from './tradingview/profitable-items/profitable-items.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatTableModule} from "@angular/material/table";
import {MatSliderModule} from "@angular/material/slider";
import {MatSortModule} from '@angular/material/sort';
import {MatButtonModule} from "@angular/material/button";
import {WhispersComponent} from './tradingview/whispers/whispers.component';
import {ClipboardModule} from "@angular/cdk/clipboard";
import {MatTooltipModule} from "@angular/material/tooltip";
import {HorizonComponent} from './tradingview/horizon/horizon.component';
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatIconModule} from "@angular/material/icon";
import {TradingviewComponent} from './tradingview/tradingview.component';
import {RouterModule} from "@angular/router";
import {GemsComponent} from './gems/gems.component';
import { TradingStackComponent } from './trading-stack/trading-stack.component';
import { VaalComponent } from './vaal/vaal.component';
import { SalesComponent } from './sales/sales.component';
import { TableviewComponent } from './sales/tableview/tableview.component';
// import { RegradingLensComponent } from './regrading-lens/regrading-lens.component';

@NgModule({
  declarations: [
    AppComponent,
    ProfitableItemsComponent,
    WhispersComponent,
    HorizonComponent,
    TradingviewComponent,
    GemsComponent,
    TradingStackComponent,
    VaalComponent,
    SalesComponent,
    TableviewComponent,
    // RegradingLensComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatTableModule,
    MatSliderModule,
    MatSortModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    ClipboardModule,
    MatTooltipModule,
    BrowserModule,
    RouterModule.forRoot([{path: '', component: TradingviewComponent},
      {path: 'leveling-gems', component: GemsComponent},
      {path: 'vaal-gems', component: VaalComponent},
      {path: 'sales', component: SalesComponent},
      // {path: 'regrading-lens', component: RegradingLensComponent},
    ])],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
