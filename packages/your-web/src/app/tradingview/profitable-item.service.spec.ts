import { TestBed } from '@angular/core/testing';

import { ProfitableItemService } from './profitable-item.service';

describe('ProfitableItemService', () => {
  let service: ProfitableItemService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProfitableItemService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
