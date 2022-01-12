import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HttpClientModule} from "@angular/common/http";
import { ProfitableItemsComponent } from './profitable-items/profitable-items.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatTableModule} from "@angular/material/table";
import {MatSliderModule} from "@angular/material/slider";
import { MatSortModule } from '@angular/material/sort';
import {MatButtonModule} from "@angular/material/button";
import { WhispersComponent } from './whispers/whispers.component';
import {ClipboardModule} from "@angular/cdk/clipboard";
import {MatTooltipModule} from "@angular/material/tooltip";

@NgModule({
  declarations: [
    AppComponent,
    ProfitableItemsComponent,
    WhispersComponent
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
    ClipboardModule,
    MatTooltipModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
