import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WhispersComponent } from './whispers.component';

describe('WhispersComponent', () => {
  let component: WhispersComponent;
  let fixture: ComponentFixture<WhispersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WhispersComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WhispersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
