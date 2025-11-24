import { TestBed } from '@angular/core/testing';

import { VaalGemsService } from './vaal-gems.service';

describe('VaalGemsService', () => {
  let service: VaalGemsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VaalGemsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
