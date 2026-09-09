import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { of } from 'rxjs';

import { WhispersComponent } from './whispers.component';
import { DirectWhisperService } from './direct-whisper.service';

describe('WhispersComponent', () => {
  let component: WhispersComponent;
  let fixture: ComponentFixture<WhispersComponent>;
  let whisperService: jasmine.SpyObj<DirectWhisperService>;

  beforeEach(async () => {
    whisperService = jasmine.createSpyObj<DirectWhisperService>('DirectWhisperService', ['direct_whisper', 'travel_to_hideout']);
    whisperService.direct_whisper.and.returnValue(of([]));
    whisperService.travel_to_hideout.and.returnValue(of([]));

    await TestBed.configureTestingModule({
      declarations: [WhispersComponent],
      providers: [{ provide: DirectWhisperService, useValue: whisperService }],
      schemas: [NO_ERRORS_SCHEMA],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WhispersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('shows Travel to Hideout label for PoE2 listings', () => {
    expect(component.actionLabel({ hideout_token: 'token' } as any)).toBe('Travel to Hideout');
  });

  it('uses travel action for PoE2 listings', () => {
    component.directWhisper({ hideout_token: 'poe2-token' } as any);

    expect(whisperService.travel_to_hideout).toHaveBeenCalledWith('poe2-token');
    expect(whisperService.direct_whisper).not.toHaveBeenCalled();
  });

  it('uses whisper action for PoE1 listings', () => {
    component.directWhisper({ whisper_token: 'poe1-token', offer_count: 3 } as any);

    expect(whisperService.direct_whisper).toHaveBeenCalledWith('poe1-token', 3);
    expect(whisperService.travel_to_hideout).not.toHaveBeenCalled();
  });
});
