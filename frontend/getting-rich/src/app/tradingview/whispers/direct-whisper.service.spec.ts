import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { DirectWhisperService } from './direct-whisper.service';
import { environment } from '../../../environments/environment';

describe('DirectWhisperService', () => {
  let service: DirectWhisperService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });
    service = TestBed.inject(DirectWhisperService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('posts PoE1 whisper payload', () => {
    service.direct_whisper('whisper-token', 4).subscribe();

    const req = httpMock.expectOne(environment.directWhisperUrl);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({
      token: 'whisper-token',
      values: [4],
      action: 'whisper',
      game: 'poe1',
    });
    req.flush({ ok: true });
  });

  it('posts PoE2 travel payload', () => {
    service.travel_to_hideout('hideout-token').subscribe();

    const req = httpMock.expectOne(environment.directWhisperUrl);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({
      token: 'hideout-token',
      hideout_token: 'hideout-token',
      action: 'travel_to_hideout',
      game: 'poe2',
    });
    req.flush({ ok: true });
  });
});
