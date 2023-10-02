import { NestFactory } from '@nestjs/core';
import { Transport } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.connectMicroservice({
    transport: Transport.NATS,
    options: {
      servers: ['nats://nats:4222'],
      queue: 'channel2',
    },
  });
  await app.startAllMicroservices();
  await app.listen(3001);
}

bootstrap();
