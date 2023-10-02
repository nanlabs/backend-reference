import { Controller, Get, UsePipes } from '@nestjs/common';
import { EventPattern } from '@nestjs/microservices';
import { AppService } from './app.service';
import {
  Resource1Created,
  PATTERN as Resource1CreatedPattern,
  Resource1CreatedValidationPipe,
} from './incomingEvents/Resource1Created.event';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @EventPattern(Resource1CreatedPattern)
  @UsePipes(new Resource1CreatedValidationPipe())
  handleResource1Created(data: Resource1Created) {
    console.log('received Resource1', data);
    this.appService.handleResource1Created(data);
  }
}
