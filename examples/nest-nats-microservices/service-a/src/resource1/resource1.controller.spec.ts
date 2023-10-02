import { Test, TestingModule } from '@nestjs/testing';
import { Resource1Controller } from './resource1.controller';
import { Resource1Service } from './resource1.service';

describe('Resource1Controller', () => {
  let controller: Resource1Controller;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [Resource1Controller],
      providers: [Resource1Service],
    }).compile();

    controller = module.get<Resource1Controller>(Resource1Controller);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
