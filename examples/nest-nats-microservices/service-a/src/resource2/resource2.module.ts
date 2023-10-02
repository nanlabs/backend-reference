import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { Resource2Controller } from './resource2.controller';
import { Resource2Service } from './resource2.service';

@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'NATS',
        transport: Transport.NATS,
        options: {
          servers: ['nats://nats:4222'],
          queue: 'channel2',
        },
      },
    ]),
  ],
  controllers: [Resource2Controller],
  providers: [Resource2Service],
})
export class Resource2Module {}
