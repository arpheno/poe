import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TradingStackComponent } from './trading-stack.component';

describe('TradingStackComponent', () => {
  let component: TradingStackComponent;
  let fixture: ComponentFixture<TradingStackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TradingStackComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TradingStackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
