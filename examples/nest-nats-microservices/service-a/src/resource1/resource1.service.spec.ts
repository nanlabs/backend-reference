import { Test, TestingModule } from '@nestjs/testing';
import { Resource1Service } from './resource1.service';

describe('Resource1Service', () => {
  let service: Resource1Service;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [Resource1Service],
    }).compile();

    service = module.get<Resource1Service>(Resource1Service);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
