import { TestBed } from '@angular/core/testing';

import { WhisperServiceService } from './whisper-service.service';

describe('WhisperServiceService', () => {
  let service: WhisperServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WhisperServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
