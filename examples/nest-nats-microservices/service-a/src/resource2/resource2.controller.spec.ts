import { Test, TestingModule } from '@nestjs/testing';
import { Resource2Controller } from './resource2.controller';
import { Resource2Service } from './resource2.service';

describe('Resource2Controller', () => {
  let controller: Resource2Controller;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [Resource2Controller],
      providers: [Resource2Service],
    }).compile();

    controller = module.get<Resource2Controller>(Resource2Controller);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
