import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Patch,
  Post,
} from '@nestjs/common';
import { CreateResource1Dto } from './dto/create-resource1.dto';
import { UpdateResource1Dto } from './dto/update-resource1.dto';
import { Resource1Service } from './resource1.service';

@Controller('resource1')
export class Resource1Controller {
  constructor(private readonly resource1Service: Resource1Service) {}

  @Post()
  create(@Body() createResource1Dto: CreateResource1Dto) {
    return this.resource1Service.create(createResource1Dto);
  }

  @Get()
  findAll() {
    return this.resource1Service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.resource1Service.findOne(id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateResource1Dto: UpdateResource1Dto,
  ) {
    return this.resource1Service.update(id, updateResource1Dto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.resource1Service.remove(id);
  }
}
