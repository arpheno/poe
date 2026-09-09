import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { of } from 'rxjs';

import { TradingStackComponent } from './trading-stack.component';
import { SearchResolveService } from '../search-resolve.service';
import { DirectWhisperService } from '../tradingview/whispers/direct-whisper.service';

describe('TradingStackComponent', () => {
  let component: TradingStackComponent;
  let fixture: ComponentFixture<TradingStackComponent>;
  let whisperService: jasmine.SpyObj<DirectWhisperService>;

  beforeEach(async () => {
    whisperService = jasmine.createSpyObj<DirectWhisperService>('DirectWhisperService', ['direct_whisper', 'travel_to_hideout']);
    whisperService.direct_whisper.and.returnValue(of([]));
    whisperService.travel_to_hideout.and.returnValue(of([]));

    await TestBed.configureTestingModule({
      declarations: [TradingStackComponent],
      providers: [
        { provide: SearchResolveService, useValue: { resolve: () => of({ result: [], query_hash: '' }) } },
        { provide: DirectWhisperService, useValue: whisperService },
      ],
      schemas: [NO_ERRORS_SCHEMA],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TradingStackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('labels PoE2 stack listing as Travel to Hideout', () => {
    expect(component.actionLabel({ hideout_token: 'token' } as any)).toBe('Travel to Hideout');
  });

  it('uses travel action for first PoE2 listing', () => {
    component.stack = [{ listing: { hideout_token: 'poe2-token' } }];

    component.getFirstWhisper();

    expect(whisperService.travel_to_hideout).toHaveBeenCalledWith('poe2-token');
    expect(whisperService.direct_whisper).not.toHaveBeenCalled();
  });
});
