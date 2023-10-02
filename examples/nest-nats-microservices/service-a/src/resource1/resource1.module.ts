import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { Resource1Controller } from './resource1.controller';
import { Resource1Service } from './resource1.service';

@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'NATS',
        transport: Transport.NATS,
        options: {
          servers: [process.env.NATS_SERVER || 'nats://nats:4222'],
        },
      },
    ]),
  ],
  controllers: [Resource1Controller],
  providers: [Resource1Service],
})
export class Resource1Module {}
