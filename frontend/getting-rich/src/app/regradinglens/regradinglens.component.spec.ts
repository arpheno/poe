import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegradinglensComponent } from './regradinglens.component';

describe('RegradinglensComponent', () => {
  let component: RegradinglensComponent;
  let fixture: ComponentFixture<RegradinglensComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegradinglensComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegradinglensComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
