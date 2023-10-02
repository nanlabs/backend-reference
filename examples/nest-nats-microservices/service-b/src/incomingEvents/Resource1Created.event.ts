import {
  ArgumentMetadata,
  BadRequestException,
  PipeTransform,
} from '@nestjs/common';
import * as Joi from 'joi';

type CreateResource1Dto = {
  id: string;
  name: string;
};

export const PATTERN = 'resource_1_created';

export class Resource1Created {
  public readonly v: number = 1;
  constructor(public readonly data: CreateResource1Dto) {}
}

const eventSchema = Joi.object({
  data: Joi.object({
    id: Joi.string().required(),
    name: Joi.string().required(),
  }).unknown(true),
}).unknown(true);

export class Resource1CreatedValidationPipe implements PipeTransform {
  transform(value: Resource1Created, metadata: ArgumentMetadata) {
    const result = eventSchema.validate(value);
    if (result.error) {
      console.log('invalid payload', value);
      console.log(result.error.message);
      throw new BadRequestException('Invalid Resource1Created event received');
    }
    return value;
  }
}
