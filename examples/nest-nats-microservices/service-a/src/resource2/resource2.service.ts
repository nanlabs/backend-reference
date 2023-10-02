import { Inject, Injectable } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { CreateResource2Dto } from './dto/create-resource2.dto';

@Injectable()
export class Resource2Service {
  constructor(@Inject('NATS') private readonly natsClient: ClientProxy) {}

  create(createResource2Dto: CreateResource2Dto) {
    return 'This action adds a new resource2';
  }

  findHelloMessage() {
    return this.natsClient.send('get_hello', {});
  }

  findOne(id: number) {
    return `This action returns a #${id} resource2`;
  }
}
