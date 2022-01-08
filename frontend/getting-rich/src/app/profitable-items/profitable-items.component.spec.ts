import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfitableItemsComponent } from './profitable-items.component';

describe('ProfitableItemsComponent', () => {
  let component: ProfitableItemsComponent;
  let fixture: ComponentFixture<ProfitableItemsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfitableItemsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfitableItemsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
