import { NestFactory } from '@nestjs/core';
import { Transport } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.connectMicroservice({
    transport: Transport.NATS,
    options: {
      servers: [process.env.NATS_SERVER || 'nats://nats:4222'],
    },
  });
  await app.startAllMicroservices();
  await app.listen(3001);
}

bootstrap();
