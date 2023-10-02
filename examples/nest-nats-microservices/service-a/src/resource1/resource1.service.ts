import { Inject, Injectable } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { v4 } from 'uuid';
import { CreateResource1Dto } from './dto/create-resource1.dto';
import { UpdateResource1Dto } from './dto/update-resource1.dto';
import {
  Resource1Created,
  PATTERN as Resource1CreatedPattern,
} from './events/created.event';

@Injectable()
export class Resource1Service {
  constructor(@Inject('NATS') private readonly natsClient: ClientProxy) {}

  create(createResource1Dto: CreateResource1Dto) {
    const id = v4();
    this.natsClient.emit<CreateResource1Dto>(
      Resource1CreatedPattern,
      new Resource1Created({ ...createResource1Dto, id }),
    );
    return 'This action adds a new resource1';
  }

  findAll() {
    return `This action returns all resource1`;
  }

  findOne(id: string) {
    return `This action returns a #${id} resource1`;
  }

  update(id: string, updateResource1Dto: UpdateResource1Dto) {
    return `This action updates a #${id} resource1`;
  }

  remove(id: string) {
    return `This action removes a #${id} resource1`;
  }
}
