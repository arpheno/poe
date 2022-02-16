import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VaalComponent } from './vaal.component';

describe('VaalComponent', () => {
  let component: VaalComponent;
  let fixture: ComponentFixture<VaalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VaalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VaalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
