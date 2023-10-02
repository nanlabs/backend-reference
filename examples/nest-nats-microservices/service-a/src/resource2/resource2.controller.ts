import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { CreateResource2Dto } from './dto/create-resource2.dto';
import { Resource2Service } from './resource2.service';

@Controller('resource2')
export class Resource2Controller {
  constructor(private readonly resource2Service: Resource2Service) {}

  @Post()
  create(@Body() createResource2Dto: CreateResource2Dto) {
    return this.resource2Service.create(createResource2Dto);
  }

  @Get()
  findHelloMessage() {
    return this.resource2Service.findHelloMessage();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.resource2Service.findOne(id);
  }
}
