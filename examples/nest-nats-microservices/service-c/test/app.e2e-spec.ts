import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import { AppModule } from './../src/app.module';
import { AppController } from './../src/app.controller';

describe('Service C message handlers (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterEach(async () => {
    await app.close();
  });

  it('returns the configured service version', () => {
    expect(app.get(AppController).getVersion()).toBe(process.env.VERSION || '0.0.21');
  });

  it('returns the service greeting', () => {
    expect(app.get(AppController).getHello()).toBe('Hello World From Service C!');
  });
});
