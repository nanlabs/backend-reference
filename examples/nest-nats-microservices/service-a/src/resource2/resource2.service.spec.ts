import { Test, TestingModule } from '@nestjs/testing';
import { Resource2Service } from './resource2.service';

describe('Resource2Service', () => {
  let service: Resource2Service;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [Resource2Service],
    }).useMocker((token) => {
      if (token === 'NATS') {
        return { emit: jest.fn(), send: jest.fn() };
      }
    }).compile();

    service = module.get<Resource2Service>(Resource2Service);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
